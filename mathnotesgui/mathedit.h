#ifndef MATHEDIT_H
#define MATHEDIT_H

#define LINE_HEIGHT 17
#define LINE_ADD 7

#include <QPlainTextEdit>

class MathEdit : public QPlainTextEdit
{
    Q_OBJECT
public:
    explicit MathEdit(QWidget *parent = 0);

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
