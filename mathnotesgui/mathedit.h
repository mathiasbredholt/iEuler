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
    void updateHeight();

signals:
    void evaluate();
    void newLinePressed();
    void deletePressed();
    void arrowsPressed(bool upArrowPressed);
    void autoRepeating(bool isAutoRepeating);

private:
    bool eventFilter(QObject *object, QEvent *event);
};

#endif // MATHEDIT_H
