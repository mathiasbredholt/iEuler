#include "mathedit.h"

MathEdit::MathEdit(QWidget *parent) : QPlainTextEdit(parent)
{
    mathEditMode = MATHMODE;
    setFocusPolicy(Qt::StrongFocus);
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setStyleSheet("QPlainTextEdit { border: none; } QPlainTextEdit:focus { border: 1px solid; }");
    setBackgroundRole(QPalette::Dark);
    setFont(parent->font());
    setPalette(parent->palette());
    installEventFilter(this);
    setTabChangesFocus(false);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    updateHeight();
    qDebug() << styleSheet();
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

        if (keyEvent->key() == Qt::Key_Return) {
            return false;
        }
        else if (keyEvent->key() == Qt::Key_Backspace) {
            return false;
        }
        emit autoRepeating(keyEvent->isAutoRepeat());
    }
    return false;
}

void MathEdit::updateHeight()
{
    setFixedHeight(ptY(LINE_ADD + blockCount() * LINE_HEIGHT));
}
