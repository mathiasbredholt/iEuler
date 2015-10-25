#ifndef CODEINPUT_H
#define CODEINPUT_H

#include <QPlainTextEdit>
#include <QTextBlock>
#include <QWidget>


class CodeInput : public QPlainTextEdit
{
    Q_OBJECT
public:
    explicit CodeInput(QWidget *parent = 0);

signals:
     void evaluateCode(CodeInput* target,QString inputString);     
     void deleteGroup(QWidget *target);
     void arrowsPressed(bool upArrowPressed);

private:
     int numberOfLines;
     bool eventFilter(QObject *object, QEvent *event);
     void addNewLine();

private slots:
     void receivedTextInput();

};

#endif // CODEINPUT_H
