﻿#ifndef PARAGRAPH_H
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
    explicit Paragraph(QWidget *parent = 0, Euler *euler = 0, Renderer *renderer = 0, int index = 0, QString mathString = "");
    int index;
    void focus();

signals:
    void newLine_triggered(int index);
    void changeFocus_triggered(bool up, int index);

private:
    Euler *euler;
    Renderer *renderer;
    MathEdit *mathEdit;
    MathWidget *mathWidget;

private slots:
    void preview();
    void evaluate();
    void receivedLatexString(int index, QString latexString);
    void arrowsPressed(bool upArrowPressed);
};

#endif // PARAGRAPH_H