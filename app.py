import os

import gradio as gr
from dotenv import load_dotenv

from llm_config import openai_client_erstellen
from qdrant_config import qdrant_client_erstellen
from rag import DEFAULT_TOP_K, beantworte_frage
from vektordg import QDRANT_COLLECTION


def erstelle_app() -> gr.Blocks:
    load_dotenv()
    openai_client = openai_client_erstellen()
    qdrant_client = qdrant_client_erstellen()

    if not qdrant_client.collection_exists(QDRANT_COLLECTION):
        qdrant_client.close()
        raise RuntimeError(
            f"Qdrant-Collection '{QDRANT_COLLECTION}' fehlt. "
            "Zuerst vektordg.py ausführen, um die Dokumente zu indexieren."
        )

    def antworten(nachricht: str, verlauf: list[dict], sprache: str) -> str:
        del verlauf
        try:
            sprache_kurz = next(
                (name for name in ("Deutsch", "English", "Tigrinya") if name in sprache),
                "Deutsch",
            )
            antwort, quellen = beantworte_frage(
                nachricht,
                openai_client,
                qdrant_client,
                top_k=DEFAULT_TOP_K,
                sprache=sprache_kurz,
            )
        except Exception as error:
            return f"Bei der Anfrage ist ein Fehler aufgetreten: {error}"

        if quellen:
            quellen_text = "\n".join(f"- {quelle}" for quelle in quellen)
            return f"{antwort}\n\n**Quellen**\n{quellen_text}"
        return antwort

    sprachauswahl = gr.Radio(
        choices=["🇩🇪 Deutsch", "🇬🇧 English", "🇪🇷 ትግርኛ"],
        value="🇩🇪 Deutsch",
        label="Antwortsprache",
        info="Deutsch und English sind bereit. Tigrinya braucht geprüfte Übersetzungsdateien.",
    )

    return gr.ChatInterface(
        fn=antworten,
        additional_inputs=[sprachauswahl],
        additional_inputs_accordion=gr.Accordion(label="Sprache auswählen", open=True),
        title="Konsulat-RAG",
        chatbot=gr.Chatbot(height=560),
        textbox=gr.Textbox(
            placeholder="Stelle eine Frage zum Generalkonsulat Eritrea ...",
            container=False,
        ),
        flagging_mode="never",
        save_history=True,
    )


def main() -> None:
    app = erstelle_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", os.getenv("GRADIO_SERVER_PORT", "7860"))),
        share=False,
        inbrowser=False,
    )


if __name__ == "__main__":
    main()