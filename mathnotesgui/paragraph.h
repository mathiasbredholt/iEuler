#ifndef PARAGRAPH_H
#define PARAGRAPH_H

#include <QWidget>
#include <QGridLayout>
#include <QDebug>
#include <QLabel>
#include <QFontMetrics>

#include "mathedit.h"
#include "mathwidget.h"
#include "euler.h"
#include "renderer.h"
#include "util.h"

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

    MathEdit *mathEdit;

    bool isEmpty();


signals:
//    void newLine_triggered(int index);
//    void nextLine_triggered();
//    void deleteLine_triggered(Paragraph *target);
//    void changeFocus_triggered(Paragraph *paragraph, bool goUp);
    void keyboardAction(int action, Paragraph *);

private:
    Euler *euler;
    Renderer *renderer;
    MathWidget *mathWidget;
    QLabel *lineNumberWidget;

    void initMathEdit();

private slots:
    void preview();
    void evaluate(int action);
    void receivedLatexString(int tabIndex, int index, QString latexString);
    void receivedPlot(int tabIndex, int index, QString path);
//    void arrowsPressed(int action);
//    void deletePressed(int action);
    void keyboardAction(int action);

public slots:
    void lineNumberChanged(QLayout *mainLayout);

};

#endif // PARAGRAPH_H
