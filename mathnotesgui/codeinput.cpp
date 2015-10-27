#include "codeinput.h"
#include <QDebug>

#define LINE_HEIGHT 17
#define LINE_ADD 7

CodeInput::CodeInput(QWidget *parent) : QPlainTextEdit(parent)
{
    setFocusPolicy(Qt::StrongFocus);
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setFixedHeight(24);
    setStyleSheet("QPlainTextEdit { border: none; background: #FAFAFA; font-size: 14px;  }");
    installEventFilter(this);
    setTabChangesFocus(false);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    connect(this, SIGNAL(textChanged()), this, SLOT(receivedTextInput()));
    setFocus();
}

bool CodeInput::eventFilter(QObject *object, QEvent *e)
{
    // Fix weird disappear bug
    if (e->type() == QEvent::Timer) return true;

    // Disable scrolling
    else if (e->type() == QEvent::Wheel) {
        e->ignore();
        return true;
    }

    // Keyboard events
    else if (object == this && e->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(e);

        if (keyEvent->key() == Qt::Key_Return && keyEvent->modifiers() == Qt::ShiftModifier) {
            addNewLine();
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Return) {
            emit evaluateCode(this, toPlainText());
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Backspace && keyEvent->modifiers() == Qt::ShiftModifier) {
            emit deleteGroup(this->parentWidget());
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
    }

    return false;
}

void CodeInput::addNewLine()
{
    textCursor().insertText("\n");
//    setFixedHeight(LINE_ADD + blockCount() * LINE_HEIGHT);
}

void CodeInput::receivedTextInput()
{
    setFixedHeight(LINE_ADD + blockCount() * LINE_HEIGHT);
    emit previewCode(this, toPlainText());
}
