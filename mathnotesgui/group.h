#ifndef GROUP_H
#define GROUP_H

#include <QWidget>
#include <QLabel>
#include <QVBoxLayout>

#include "codeinput.h"

class Group : public QWidget
{
    Q_OBJECT
public:
    explicit Group(QWidget *parent = 0);

    CodeInput* input;
    QLabel* output;


signals:
    void deleteGroup(Group* target);

public slots:
    void deleteCode();
    void outputReady();
};

#endif // GROUP_H
