#include "group.h"

Group::Group(QWidget *parent, int index) : QWidget(parent)
{
    this->index = index;
    setFocusPolicy(Qt::NoFocus);
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setFixedHeight(128);
    setLayout(new QVBoxLayout());

    input = new CodeInput(this);
    layout()->addWidget(input);

    output = new MathRenderer(this);
    layout()->addWidget(output->label);
//    output = new QLabel(this);
//    output->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
}

void Group::outputReady(int lineIndex, QString latexString)
{
    if (lineIndex == index)
        output->latexString = latexString;

    MathRenderer::renderQueue.enqueue(output);
        if (!MathRenderer::isRendering && MathRenderer::isReady) MathRenderer::render();
//    output->setPixmap(QPixmap("mathnotes.png"));
}
