pyinstaller ^
--name "AuraService" ^
--onefile ^
--windowed ^
--add-data "attention_aware_classifier.joblib:." ^
--add-data "aura_log.csv:." ^
--add-data "credentials.json:." ^
--add-data "token.json:." ^
--add-data "aura_memory_db:aura_memory_db" ^
--hidden-import "uvicorn.logging" ^
--hidden-import "uvicorn.lifespan.on" ^
--hidden-import "chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2" ^
--hidden-import "onnxruntime" ^
--hidden-import "tokenizers" ^
--collect-all "chromadb" ^
prediction_api.py
