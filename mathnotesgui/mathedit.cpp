#include "mathedit.h"

MathEdit::MathEdit(QWidget *parent) : QPlainTextEdit(parent)
{
    mathEditMode = MATHMODE;
    setFocusPolicy(Qt::StrongFocus);
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setFixedHeight(24);
    setStyleSheet("QPlainTextEdit { border: none; background: #EEE; font-size: 14px;  }");
    installEventFilter(this);
    setTabChangesFocus(false);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    //    setFixedHeight(LINE_ADD + blockCount() * LINE_HEIGHT);
}

void MathEdit::setMode(int mathEditMode)
{
    if (this->mathEditMode != mathEditMode) {
        this->mathEditMode = mathEditMode;
        if (mathEditMode == MATHMODE) {
            setStyleSheet("QPlainTextEdit { border: none; background: #EEE; font-size: 14px;  }");
        }
        else if (mathEditMode == TEXTMODE) {
            setStyleSheet("QPlainTextEdit { border: none; background: #DDD; font-size: 14px;  }");
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
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Return) {
            emit evaluate();
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Backspace && keyEvent->modifiers() == Qt::ShiftModifier) {
            emit deletePressed();
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Up) {
            if (textCursor().blockNumber() == 0) {
                emit arrowsPressed(true);
                return true;
            }
        }
        else if (keyEvent->key() == Qt::Key_Down) {
            if (textCursor().blockNumber() == blockCount() - 1) {
                emit arrowsPressed(false);
                return true;
            }
        }
        emit autoRepeating(keyEvent->isAutoRepeat());
    }

    else if (object == this && event->type() == QEvent::KeyRelease) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);
        emit autoRepeating(keyEvent->isAutoRepeat());
    }
    return false;
}
