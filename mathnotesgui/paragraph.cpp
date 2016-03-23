#include "paragraph.h"

Paragraph::Paragraph(QWidget *parent,
                     Euler *euler,
                     Renderer *renderer,
                     int tabIndex,
                     int index,
                     QString mathString) :QWidget(parent)
{
    this->euler = euler;
    this->renderer = renderer;
    this->tabIndex = tabIndex;
    this->index = index;

    setPalette(parent->palette());
    setFont(parent->font());

    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
//    setFixedHeight(128);

    setLayout(new QVBoxLayout());

    connect(euler, SIGNAL(receivedLatexString(int, int, QString)), this, SLOT(receivedLatexString(int, int, QString)));

    initMathEdit();

    mathWidget = new MathWidget(this);
    layout()->addWidget(mathWidget);

//    layout()->addWidget(renderer->webengine);

    mathEdit->setPlainText(mathString);
}

void Paragraph::focus()
{
    mathEdit->setFocus();
}

void Paragraph::initMathEdit()
{
    mathEdit = new MathEdit(this);
    connect(mathEdit, SIGNAL(textChanged()), this, SLOT(preview()));
    connect(mathEdit, SIGNAL(evaluate()), this, SLOT(evaluate()));
    connect(mathEdit, SIGNAL(arrowsPressed(bool)), this, SLOT(arrowsPressed(bool)));
    connect(mathEdit, SIGNAL(deletePressed()), this, SLOT(deletePressed()));
    connect(mathEdit, SIGNAL(autoRepeating(bool)), renderer, SLOT(toggleRendering(bool)));
    layout()->addWidget(mathEdit);
}

void Paragraph::preview()
{
    QString mathString = mathEdit->toPlainText();
    mathEdit->updateHeight();
    if (mathString.indexOf('%') == 0) {
        mathEdit->setMode(MathEdit::TEXTMODE);
    } else {
        mathEdit->setMode(MathEdit::MATHMODE);
    }
    euler->sendMathString(tabIndex, index, mathString, false);
}

void Paragraph::evaluate()
{
    QString mathString = mathEdit->toPlainText();
    euler->sendMathString(tabIndex, index, mathString, true);
    emit newLine_triggered(index);
}

void Paragraph::receivedLatexString(int tabIndex, int index, QString latexString)
{
    if (tabIndex == this->tabIndex && index == this->index && mathWidget->latexString != latexString) {
        mathWidget->latexString = latexString;
        renderer->render(mathWidget);
    }
}

void Paragraph::arrowsPressed(bool upArrowPressed)
{
    emit changeFocus_triggered(upArrowPressed, index);
}

void Paragraph::deletePressed()
{
    emit deleteLine_triggered(this);
}
