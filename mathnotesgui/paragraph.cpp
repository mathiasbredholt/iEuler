#include "paragraph.h"

Paragraph::Paragraph(QWidget *parent, Euler *euler, Renderer *renderer, int index, QString mathString) : QWidget(parent)
{
    this->euler = euler;
    this->renderer = renderer;
    this->index = index;

    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setFixedHeight(128);
    setLayout(new QVBoxLayout());

    mathEdit = new MathEdit(this);

    mathWidget = new MathWidget(this);

    layout()->addWidget(mathEdit);
    layout()->addWidget(mathWidget);

    connect(mathEdit, SIGNAL(textChanged()), this, SLOT(preview()));
    connect(mathEdit, SIGNAL(evaluate()), this, SLOT(evaluate()));
    connect(mathEdit, SIGNAL(arrowsPressed(bool)), this, SLOT(arrowsPressed(bool)));
    connect(mathEdit, SIGNAL(autoRepeating(bool)), renderer, SLOT(toggleRendering(bool)));
    connect(euler, SIGNAL(receivedLatexString(int, QString)), this, SLOT(receivedLatexString(int, QString)));

    mathEdit->setPlainText(mathString);
}

void Paragraph::focus()
{
    mathEdit->setFocus();
}

void Paragraph::preview()
{
    QString mathString = mathEdit->toPlainText();
    euler->sendMathString(index, mathString, false);
}

void Paragraph::evaluate()
{
    QString mathString = mathEdit->toPlainText();
    euler->sendMathString(index, mathString, true);
    emit newLine_triggered(index);
}

void Paragraph::receivedLatexString(int index, QString latexString)
{
    if (index == this->index && mathWidget->latexString != latexString) {
        mathWidget->latexString = latexString;
        renderer->render(mathWidget);
    }
}

void Paragraph::arrowsPressed(bool upArrowPressed)
{
    emit changeFocus_triggered(upArrowPressed, index);
}
