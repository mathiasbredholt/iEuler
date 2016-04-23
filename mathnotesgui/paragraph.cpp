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

    setLayout(new QHBoxLayout());
    layout()->setMargin(0);

    lineNumberWidget = new QLabel("1");
    lineNumberWidget->setFont(parent->font());
    lineNumberWidget->setFixedSize(ptX(8), QFontMetrics(font()).height() + ptY(10));
    layout()->addWidget(lineNumberWidget);
    layout()->setAlignment(lineNumberWidget, Qt::AlignTop);

    QWidget *container = new QWidget();
    container->setLayout(new QVBoxLayout());
    container->layout()->setMargin(0);

    connect(euler, SIGNAL(receivedLatexString(int, int, QString)), this, SLOT(receivedLatexString(int, int, QString)));
    connect(euler, SIGNAL(receivedPlot(int,int,QString)), this, SLOT(receivedPlot(int,int,QString)));

    initMathEdit();
    container->layout()->addWidget(mathEdit);

    mathWidget = new MathWidget(this);
    container->layout()->addWidget(mathWidget);

    mathEdit->setPlainText(mathString);

    preview();

    layout()->addWidget(container);
    layout()->setAlignment(container, Qt::AlignTop);
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
    if ((action == MathEdit::EVAL_AND_CONTINUE || action == MathEdit::EVAL_IN_PLACE) && !isEmpty()) {
        QString mathString = mathEdit->toPlainText();
        euler->sendMathString(tabIndex, index, mathString, true);
    }
}

void Paragraph::keyboardAction(int action)
{
    emit keyboardAction(action, this);
}

void Paragraph::lineNumberChanged(QLayout *mainLayout)
{
    qDebug() << mainLayout->indexOf(this) + 1;
    lineNumberWidget->setNum(mainLayout->indexOf(this) + 1);
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

bool Paragraph::isEmpty()
{
    return mathEdit->toPlainText().length() == 0;
}
