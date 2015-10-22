#include "group.h"

Group::Group(QWidget *parent, int index) : QWidget(parent)
{
    this->index = index;

    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    QVBoxLayout *vlayout = new QVBoxLayout();
    input = new CodeInput(this);
//    output = new QLabel(this);
//    output->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    output = new MathRenderer();
    vlayout->addWidget(input);
    vlayout->addWidget(output->view);
    setLayout(vlayout);
}

void Group::outputReady(int lineIndex)
{
    output->render(QString("3+4"));
//    if (lineIndex == index)
//    output->setPixmap(QPixmap("mathnotes.png"));
}
