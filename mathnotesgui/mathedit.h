#ifndef MATHEDIT_H
#define MATHEDIT_H

#define LINE_HEIGHT 20
#define LINE_ADD 7

#include <QPlainTextEdit>
#include "util.h"

class MathEdit : public QPlainTextEdit
{
    Q_OBJECT
public:
    explicit MathEdit(QWidget *parent = 0);
    int mathEditMode;
    void setMode(int mathEditMode);

    static const int MATHMODE = 0;
    static const int TEXTMODE = 1;

    static const int EVAL_IN_PLACE = 0;
    static const int EVAL_AND_CONTINUE = 1;
    static const int MOVE_UP = 2;
    static const int MOVE_DOWN = 3;
    static const int INSERT_ABOVE = 4;
    static const int INSERT_BELOW = 5;
    static const int DELETE_LINE = 6;

    void updateHeight();

signals:
    void keyboardAction(int action);

private:
    bool eventFilter(QObject *object, QEvent *event);
};

#endif // MATHEDIT_H
