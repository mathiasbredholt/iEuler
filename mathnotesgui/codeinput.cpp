#include "codeinput.h"
#include <QDebug>

#define LINE_HEIGHT 17
#define LINE_ADD 7

CodeInput::CodeInput(QWidget *parent) : QPlainTextEdit(parent)
{
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setFixedHeight(24);
    setStyleSheet("QPlainTextEdit { border: none; background: #DDD; font-size: 14px;  }");
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
    else if (object == this && e->type() == QEvent::Wheel) e->ignore();

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
    textCursor().insertText("\n");
//    setFixedHeight(LINE_ADD + blockCount() * LINE_HEIGHT);
}

void CodeInput::removeLine()
{
//    QString text;
//    int index, size;

//    qDebug() << textCursor().position() - textCursor().block().position();
//    if (textCursor().position() - textCursor().block().position() == 0) {
//        // obtain the current text (whole)
//        text = toPlainText();
//        index = text.lastIndexOf('\n');
//        size = text.size();

//        qDebug() << text;

//        // Last line is not the first
//        if (index != -1)
//            text.remove(index, size - index);
//        // Last line = first line
//        else
//           text.remove(0, size );

//        qDebug() << text;
//        setPlainText(text);
//        moveCursor( QTextCursor::End, QTextCursor::MoveAnchor );

//        // scale

//    }
}

void CodeInput::receivedTextInput()
{
    setFixedHeight(LINE_ADD + blockCount() * LINE_HEIGHT);
    emit previewCode(this, toPlainText());
}

//QSize CodeInput::sizeHint() const
//{
//    return QSize(128, 24);
//}

//QSize CodeInput::minimumSizeHint() const
//{
//    return QSize(128, 24);
//}
