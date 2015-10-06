#include "codeinput.h"

CodeInput::CodeInput(QWidget *parent) : QPlainTextEdit(parent)
{
    setStyleSheet("QPlainTextEdit { border: none; background: #DDD; }");
    installEventFilter(this);
    setTabChangesFocus(false);
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
            emit deleteGroup(this->parentWidget());
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Up) {
            emit arrowsPressed(true);
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Down) {
            emit arrowsPressed(false);
            return true;
        }
    }
    return false;
}
