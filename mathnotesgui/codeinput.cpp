#include "codeinput.h"

CodeInput::CodeInput(QWidget *parent) : QPlainTextEdit(parent)
{
    setStyleSheet("QPlainTextEdit { border: none; }");
    installEventFilter(this);
    setTabChangesFocus(true);
    setMaximumHeight(24);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
}

bool CodeInput::eventFilter(QObject *object, QEvent *e)
{
    if (object == this && e->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(e);
        if (keyEvent->key() == Qt::Key_Return) {
            emit evaluateCode(this, this->textCursor().block().text());
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Backspace && keyEvent->modifiers() == Qt::ShiftModifier) {
            emit deleteCode();
            return true;
        }
    }
    return false;
}
