from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Lista de palabras relacionadas con ventas
palabras_ventas = ['venta', 'vendo', 'compro', 'jugosa', 'se vende', 'barato', 'publicidad', 'promoción', 'oferta']

# Comando /start para verificar que el bot está activo
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo. Vigilando mensajes de ventas...")

# Función para manejar mensajes
async def filtrar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower() if update.message.text else ""
    
    if any(palabra in texto for palabra in palabras_ventas):
        try:
            # Intentar borrar el mensaje
            await update.message.delete()
            # Avisar al grupo que se borró un mensaje de venta
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"🚫 Mensaje eliminado por contener contenido de venta."
            )
        except Exception as e:
            print(f"Error al borrar mensaje: {e}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ No tengo permisos para borrar mensajes."
            )

def main():
    TOKEN = "7972119530:AAGyIIz1cZiK2DLAPmkksrqV75oU3pqry4A"  # Pon aquí tu token del bot
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filtrar_mensajes))

    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
