#include "codeinput.h"
#include <QDebug>

CodeInput::CodeInput(QWidget *parent) : QPlainTextEdit(parent)
{
    numberOfLines = 1;
    setMaximumHeight(24);
    setStyleSheet("QPlainTextEdit { border: none; background: #DDD; }");
    installEventFilter(this);
    setTabChangesFocus(false);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    connect(this, SIGNAL(textChanged()), this, SLOT(receivedTextInput()));
}

bool CodeInput::eventFilter(QObject *object, QEvent *e)
{
    // Fix weird disappear bug
    if (e->type() == QEvent::Timer) return true;

    // Disable scrolling
    else if (e->type() == QEvent::Wheel) return true;

    // Keyboard events
    else if (object == this && e->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(e);

        if (keyEvent->key() == Qt::Key_Return && keyEvent->modifiers() == Qt::ShiftModifier) {
            addNewLine();
            return true;
        }
        else if (keyEvent->key() == Qt::Key_Return) {
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
            qDebug() << textCursor().blockNumber();
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
    numberOfLines++;
    setMaximumHeight(8 + numberOfLines * 16);
    textCursor().insertText("\n");
}

void CodeInput::receivedTextInput()
{
    emit evaluateCode(this, toPlainText());
}
