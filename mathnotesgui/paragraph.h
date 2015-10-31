#ifndef PARAGRAPH_H
#define PARAGRAPH_H

#include <QWidget>
#include <QVBoxLayout>

#include "mathedit.h"
#include "mathwidget.h"
#include "euler.h"
#include "renderer.h"

class Paragraph : public QWidget
{
    Q_OBJECT
public:
    explicit Paragraph(QWidget *parent = 0,
                       Euler *euler = 0,
                       Renderer *renderer = 0,
                       int tabIndex = 0,
                       int index = 0,
                       QString mathString = "");
    int tabIndex;
    int index;
    void focus();

signals:
    void newLine_triggered(int index);
    void deleteLine_triggered(Paragraph *target);
    void changeFocus_triggered(bool up, int index);

private:
    Euler *euler;
    Renderer *renderer;
    MathEdit *mathEdit;
    MathWidget *mathWidget;

    void initMathEdit();

private slots:
    void preview();
    void evaluate();
    void receivedLatexString(int tabIndex, int index, QString latexString);
    void arrowsPressed(bool upArrowPressed);
    void deletePressed();
};

#endif // PARAGRAPH_H
