# client/memory_service.py

import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import uuid

# --- CONFIGURATION ---
# Path where ChromaDB will store the memory data (the vectors)
PERSIST_PATH = "client/aura_memory_db"
# Name of our memory collection
COLLECTION_NAME = "activity_memories"
# Model to convert text into vectors (a good, fast, small model for local use)
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' 

class MemoryService:
    def __init__(self):
        # 1. Initialize the ChromaDB Client
        # PersistentClient ensures data is saved to disk
        self.client = chromadb.PersistentClient(path=PERSIST_PATH)
        
        # 2. Initialize the Embedding Model
        # This model turns the log data into high-dimensional vectors
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # 3. Get or Create the Collection
        # Chroma will use the SentenceTransformer for embedding automatically
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def generate_document_text(self, row):
        """Generates a rich, descriptive text string from a single log row."""
        return (
            f"User was '{row['user_state']}' for 60 seconds. "
            f"Active app was '{row['active_app']}'. "
            f"Typing: {row['key_count']} keys, Mouse: {int(row['mouse_distance'])}px. "
            f"Calendar state: '{row['calendar_state']}'. "
            f"Context: {row['active_app']} use while {row['calendar_state']}."
        )

    def save_memory(self, log_data_df):
        """
        Takes new log data (a Pandas DataFrame), converts rows to descriptive text,
        and saves them as vectors in the database.
        """
        # We need unique IDs for each entry (memory)
        ids = [str(uuid.uuid4()) for _ in log_data_df.index]
        
        # Generate the descriptive text from the row data
        documents = [self.generate_document_text(row) for index, row in log_data_df.iterrows()]
        
        # Prepare metadata (useful for filtering/context)
        metadatas = log_data_df.to_dict('records')

        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Saved {len(ids)} new memories to ChromaDB.")
        except Exception as e:
            print(f"❌ Error saving to ChromaDB: {e}")

    def recall_context(self, current_state_text, n_results=5):
        """
        Queries the database for past memories most similar to the current activity.
        Returns a list of the top N most relevant memory documents.
        """
        try:
            results = self.collection.query(
                query_texts=[current_state_text],
                n_results=n_results,
                include=['documents', 'metadatas']
            )
            
            # Extract the memory text for context injection
            context_documents = results.get('documents', [[]])[0]
            
            return context_documents
            
        except Exception as e:
            print(f"❌ Error recalling context from ChromaDB: {e}")
            return []

if __name__ == '__main__':
    # --- Simple Test and Demo ---
    memory_service = MemoryService()
    
    # Create a small dummy DataFrame of new data to log
    new_logs = pd.DataFrame({
        'user_state': ['focused', 'distracted'],
        'active_app': ['PyCharm', 'TikTok'],
        'key_count': [800, 10],
        'mouse_distance': [200, 3500],
        'calendar_state': ['free', 'free']
    })
    
    # Save the dummy data as memories
    memory_service.save_memory(new_logs)
    
    # Test recalling memory (Aura's prediction step)
    current_activity = "I am using VSCode and typing quickly while my calendar is free. I feel very productive."
    recalled_memories = memory_service.recall_context(current_activity, n_results=1)
    
    print("\n--- Recalled Context (Long-Term Memory) ---")
    if recalled_memories:
        print(f"Current Activity: {current_activity}")
        print(f"Most Relevant Past Memory: {recalled_memories[0]}")
    else:
        print("No memories recalled.")
