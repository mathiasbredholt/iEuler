#include "paragraph.h"

Paragraph::Paragraph(QWidget *parent,
                     Euler *euler,
//                     Renderer *renderer,
                     int tabIndex,
                     int index,
                     QString mathString) :QWidget(parent)
{
    this->euler = euler;
//    this->renderer = renderer;
    this->tabIndex = tabIndex;
    this->index = index;
    this->mathString = mathString;

    setFocusPolicy(Qt::NoFocus);
    setPalette(parent->palette());
    setFont(parent->font());

    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
//    setFixedHeight(128);

    QGridLayout *gridLayout = new QGridLayout();

    gridLayout->setMargin(0);

    lineNumberWidget = new QLabel("1");
    lineNumberWidget->setFont(parent->font());
    lineNumberWidget->setFixedWidth(ptX(16));
    gridLayout->addWidget(lineNumberWidget, 0, 0);
    gridLayout->setAlignment(lineNumberWidget, Qt::AlignVCenter);

    connect(euler, SIGNAL(receivedLatexString(int, int, QString)), this, SLOT(receivedLatexString(int, int, QString)));
    connect(euler, SIGNAL(receivedPlot(int,int,QString)), this, SLOT(receivedPlot(int,int,QString)));

    initMathEdit();
    gridLayout->addWidget(mathEdit, 0, 1);

//    mathWidget = new MathWidget(this);
//    gridLayout->addWidget(mathWidget, 1, 1);
//    svgWidget = new QSvgWidget(this);
//    gridLayout->addWidget(svgWidget, 1, 1);
    mathWidget = new QLabel(this);
    gridLayout->addWidget(mathWidget, 1, 1);

    mathEdit->setPlainText(mathString);

    preview();
    setLayout(gridLayout);
}

void Paragraph::focus()
{
    mathEdit->setFocus();
}

void Paragraph::initMathEdit()
{
    mathEdit = new MathEdit(this);
    connect(mathEdit, SIGNAL(textChanged()), this, SLOT(preview()));
    connect(mathEdit, SIGNAL(keyboardAction(int)), this, SLOT(evaluate(int)));
    connect(mathEdit, SIGNAL(keyboardAction(int)), this, SLOT(keyboardAction(int)));
}

void Paragraph::preview()
{
    mathString = mathEdit->toPlainText();

    mathEdit->updateHeight();

    if (mathString.indexOf('%') == 0) {
        mathEdit->setMode(MathEdit::TEXTMODE);
    } else {
        mathEdit->setMode(MathEdit::MATHMODE);
    }

    euler->sendMathString(tabIndex, index, mathString, false);
}

void Paragraph::evaluate(int action)
{
    mathString = mathEdit->toPlainText();

    if ((action == MathEdit::EVAL_AND_CONTINUE || action == MathEdit::EVAL_IN_PLACE) && !isEmpty()) {
        euler->sendMathString(tabIndex, index, mathString, true);
    }
}

void Paragraph::keyboardAction(int action)
{
    emit keyboardAction(action, this);
}

void Paragraph::lineNumberChanged(int tabIndex, QLayout *mainLayout)
{
    if (tabIndex == this->tabIndex) {
        index = mainLayout->indexOf(this);
        lineNumberWidget->setNum(mainLayout->indexOf(this) + 1);
    }
}

void Paragraph::receivedLatexString(int tabIndex, int index, QString latexString)
{
    if (tabIndex == this->tabIndex && index == this->index && this->latexString != latexString) {
        this->latexString = latexString;
//        renderer->render(this);
        emit doRender(this);
    }
}

void Paragraph::receivedPlot(int tabIndex, int index, QString path)
{
    if (tabIndex == this->tabIndex && index == this->index) {
//        mathWidget->loadPlot(path);
    }
}

bool Paragraph::isEmpty()
{
    return mathEdit->toPlainText().length() == 0;
}

