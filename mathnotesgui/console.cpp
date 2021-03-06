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

    append("<p style='color:black'>" + QDir::currentPath() + "</p>");
}

void Console::receivedMsg(QString msg)
{
    append("<p style='color:black'>" + msg.simplified() + "</p>");
    verticalScrollBar()->setValue(verticalScrollBar()->maximum());
}

void Console::receivedError(QString msg)
{
    qDebug() << "eerrrrr";
    append("<p style='color:red'>" + msg.replace("\n","<br>") + "</p>");
    verticalScrollBar()->setValue(verticalScrollBar()->maximum());
}
