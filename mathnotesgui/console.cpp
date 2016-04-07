#include "console.h"

Console::Console(QWidget *parent) : QTextEdit(parent)
{
//    setLayout(new QVBoxLayout());
//    label = new QTextEdit();
//    label->setFont(QFont("Monaco", 9));
//    QScrollArea *scrollArea = new QScrollArea(label);
//    layout()->addWidget(scrollArea);

    setFixedHeight(ptY(80));
    setReadOnly(true);
    setFont(QFont("Monaco", 10));
}

void Console::receivedMsg(QString msg)
{
    append(msg.simplified());
    ensureCursorVisible();
}

void Console::receivedError(QString msg)
{
    append("<p style='color:red'>" + msg.replace("\n","<br>") + "</p>");
    ensureCursorVisible();
}
