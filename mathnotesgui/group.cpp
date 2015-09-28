#include "group.h"

Group::Group(QWidget *parent) : QWidget(parent)
{
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    QVBoxLayout *vlayout = new QVBoxLayout();
    input = new CodeInput();
    output = new QLabel();
    output->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    vlayout->addWidget(input);
    setLayout(vlayout);
    QObject::connect(input, SIGNAL(deleteCode()), this, SLOT(deleteCode()));
}

void Group::deleteCode()
{
    emit deleteGroup(this);
}

void Group::outputReady()
{
    output->setText("<img src='mathnotes.png' />");
    layout()->addWidget(output);
}
