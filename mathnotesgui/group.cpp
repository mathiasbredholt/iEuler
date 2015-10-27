#include "group.h"

Group::Group(QWidget *parent, int index, QString cmd) : QWidget(parent)
{
    this->index = index;
    setFocusPolicy(Qt::NoFocus);
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setFixedHeight(112);
    setLayout(new QVBoxLayout());

    input = new CodeInput(this);
    input->setPlainText(cmd);
    layout()->addWidget(input);

    output = new MathRenderer();
    layout()->addWidget(output->view);

//    output = new QLabel(this);
//    output->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
}

void Group::outputReady(int lineIndex, QString latexString)
{
    if (lineIndex == index)
        output->render(latexString);
//    output->setPixmap(QPixmap("mathnotes.png"));
}
