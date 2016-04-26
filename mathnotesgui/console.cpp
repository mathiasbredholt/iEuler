#include "console.h"

Console::Console(QWidget *parent) : QTextEdit(parent)
{
//    setLayout(new QVBoxLayout());
//    label = new QTextEdit();
//    label->setFont(QFont("Monaco", 9));
//    QScrollArea *scrollArea = new QScrollArea(label);
//    layout()->addWidget(scrollArea);

    setFocusPolicy(Qt::ClickFocus);
    setReadOnly(true);
    setFont(QFont("Monaco", 10));
}

void Console::receivedMsg(QString msg)
{
    append("<p style='color:black'>" + msg.simplified() + "</p>");
    textCursor().setPosition(toPlainText().length());
    ensureCursorVisible();
}

void Console::receivedError(QString msg)
{
    append("<p style='color:red'>" + msg.replace("\n","<br>") + "</p>");
    textCursor().setPosition(toPlainText().length());
    ensureCursorVisible();
}
