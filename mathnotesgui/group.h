#ifndef GROUP_H
#define GROUP_H

#include <QWidget>
#include <QLabel>
#include <QVBoxLayout>
#include <QPixmap>
#include "codeinput.h"
#include "mathrenderer.h"

class Group : public QWidget
{
    Q_OBJECT
public:
    explicit Group(QWidget *parent = 0, int index = 0);
    int index;
    CodeInput* input;

private:
    // QLabel* output;
    MathRenderer *output;

signals:

public slots:
    void outputReady(int lineIndex, QString latexString);
};

#endif // GROUP_H
