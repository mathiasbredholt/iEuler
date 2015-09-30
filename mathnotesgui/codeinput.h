#ifndef CODEINPUT_H
#define CODEINPUT_H

#include <QPlainTextEdit>
#include <QTextBlock>


class CodeInput : public QPlainTextEdit
{
    Q_OBJECT
public:
    explicit CodeInput(QWidget *parent = 0);

signals:
     void evaluateCode(CodeInput* target,QString inputString);
     void deleteCode();

private:
     bool eventFilter(QObject *object, QEvent *event);
};

#endif // CODEINPUT_H