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
//    QSize sizeHint() const;
//    QSize minimumSizeHint() const;

signals:
    void previewCode(CodeInput* target, QString inputString);
    void evaluateCode(CodeInput* target,QString inputString);
    void deleteGroup(QWidget *target);
    void arrowsPressed(bool upArrowPressed);

private:
     bool eventFilter(QObject *object, QEvent *event);
     void addNewLine();
     void removeLine();

private slots:
     void receivedTextInput();

};

#endif // CODEINPUT_H
