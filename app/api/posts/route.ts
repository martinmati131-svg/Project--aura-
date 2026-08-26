import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

export async function POST(req: Request) {
  try {
    const { title, slug, content, userId, metadata } = await req.json();

    if (!title || !content) {
      return NextResponse.json(
        { error: "Title and content are required." },
        { status: 400 }
      );
    }

    const { data, error } = await supabase
      .from("posts")
      .insert([
        {
          title,
          slug: slug || title.toLowerCase().replace(/ /g, "-").replace(/[^\w-]+/g, ""),
          content,
          user_id: userId || null,
          metadata: metadata || {},
        },
      ])
      .select();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 400 });
    }

    return NextResponse.json({ success: true, post: data[0] });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Internal server error" },
      { status: 500 }
    );
  }
}
