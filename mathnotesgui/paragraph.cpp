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

    setFocusPolicy(Qt::NoFocus);
    setPalette(parent->palette());
    setFont(parent->font());

    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
//    setFixedHeight(128);

    setLayout(new QVBoxLayout());

    connect(euler, SIGNAL(receivedLatexString(int, int, QString)), this, SLOT(receivedLatexString(int, int, QString)));
    connect(euler, SIGNAL(receivedPlot(int,int,QString)), this, SLOT(receivedPlot(int,int,QString)));

    initMathEdit();

    mathWidget = new MathWidget(this);
    layout()->addWidget(mathWidget);

//    layout()->addWidget(renderer->webengine);

    mathEdit->setPlainText(mathString);
    preview();
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
//    connect(mathEdit, SIGNAL(keyboardAction(int)), this, SLOT(deletePressed(int)));
    connect(mathEdit, SIGNAL(keyboardAction(int)), this, SLOT(keyboardAction(int)));
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

void Paragraph::evaluate(int action)
{
    if (action == MathEdit::EVAL_AND_CONTINUE || action == MathEdit::EVAL_IN_PLACE) {
        QString mathString = mathEdit->toPlainText();
        euler->sendMathString(tabIndex, index, mathString, true);
    }
}

void Paragraph::keyboardAction(int action)
{
    emit keyboardAction(action, this);
}

void Paragraph::receivedLatexString(int tabIndex, int index, QString latexString)
{
    if (tabIndex == this->tabIndex && index == this->index && mathWidget->latexString != latexString) {
        mathWidget->latexString = latexString;
        renderer->render(mathWidget);
    }
}

void Paragraph::receivedPlot(int tabIndex, int index, QString path)
{
    if (tabIndex == this->tabIndex && index == this->index) {
        mathWidget->loadPlot(path);
    }
}

//void Paragraph::arrowsPressed(int action)
//{
//    emit changeFocus_triggered(this, action);
//}

//void Paragraph::deletePressed(int action)
//{
//    if (action == MathEdit::DELETE_LINE) emit deleteLine_triggered(this);
//}
