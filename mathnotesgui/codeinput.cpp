#include "codeinput.h"

CodeInput::CodeInput(QWidget *parent) : QPlainTextEdit(parent)
{
    this->setStyleSheet("QPlainTextEdit { border: none; }");
    this->installEventFilter(this);
    this->setTabChangesFocus(true);
    this->setMaximumHeight(24);
    this->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
}

bool CodeInput::eventFilter(QObject *object, QEvent *e)
{
    if (object == this && e->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(e);
        if (keyEvent->key() == Qt::Key_Return) {
            emit evaluateCode(this->textCursor().block().text());
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Backspace && keyEvent->modifiers() == Qt::ShiftModifier) {
            emit deleteCode(this);
            return true;
        }
    }
    return false;
}
