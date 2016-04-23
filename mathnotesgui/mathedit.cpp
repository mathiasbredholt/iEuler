#include "mathedit.h"

MathEdit::MathEdit(QWidget *parent) : QPlainTextEdit(parent)
{
    setStyleSheet("border: none;");
    mathEditMode = MATHMODE;
    setFocusPolicy(Qt::StrongFocus);
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setBackgroundRole(QPalette::Dark);
    setFont(parent->font());
    setPalette(parent->palette());
    installEventFilter(this);
    setTabChangesFocus(false);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    updateHeight();
}

void MathEdit::setMode(int mathEditMode)
{
    if (this->mathEditMode != mathEditMode) {
        this->mathEditMode = mathEditMode;
        if (mathEditMode == MATHMODE) {

            setStyleSheet("QPlainTextEdit { border: none; } QPlainTextEdit:focus { border: 1px solid; }");
        }
        else if (mathEditMode == TEXTMODE) {
            setStyleSheet("QPlainTextEdit { border: none; } QPlainTextEdit:focus { border: 1px solid; }");
        }
    }
}


bool MathEdit::eventFilter(QObject *object, QEvent *event)
{
    // Fix weird disappear bug
    if (event->type() == QEvent::Timer) return true;

    // Disable scrolling
    else if (event->type() == QEvent::Wheel) {
        event->ignore();
        return true;
    }
    // Keyboard events
    else if (object == this && event->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);

        if (keyEvent->key() == Qt::Key_Return && keyEvent->modifiers() == Qt::ShiftModifier) {
            emit keyboardAction(EVAL_IN_PLACE);
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Return && keyEvent->modifiers() == Qt::ControlModifier) {
            emit keyboardAction(EVAL_AND_CONTINUE);
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Backspace && keyEvent->modifiers() == Qt::ShiftModifier) {
            emit keyboardAction(DELETE_LINE);
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Up && keyEvent->modifiers() & Qt::ControlModifier && keyEvent->modifiers() & Qt::KeypadModifier) {
            emit keyboardAction(INSERT_ABOVE);
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Down && keyEvent->modifiers() & Qt::ControlModifier && keyEvent->modifiers() & Qt::KeypadModifier) {
            emit keyboardAction(INSERT_BELOW);
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Up) {
            if (textCursor().blockNumber() == 0) {
                emit keyboardAction(MOVE_UP);
                return true;
            }
        }
        else if (keyEvent->key() == Qt::Key_Down) {
            if (textCursor().blockNumber() == blockCount() - 1) {
                emit keyboardAction(MOVE_DOWN);
                return true;
            }
        }
//        emit autoRepeating(keyEvent->isAutoRepeat());
    }
    else if (object == this && event->type() == QEvent::KeyRelease) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);

        if (keyEvent->key() == Qt::Key_Return) {
            return false;
        }
        else if (keyEvent->key() == Qt::Key_Backspace) {
            return false;
        }
//        emit autoRepeating(keyEvent->isAutoRepeat());
    }
    else if (object == this && event->type() == QEvent::FocusIn) {
        setStyleSheet("border: 1px solid;");
    }
    else if (object == this && event->type() == QEvent::FocusOut) {
        setStyleSheet("border: none;");
    }

    return false;
}

void MathEdit::updateHeight()
{
    setFixedHeight(ptY(LINE_ADD + blockCount() * LINE_HEIGHT));
}
