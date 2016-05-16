#ifndef CONSOLE_H
#define CONSOLE_H

#include <QWidget>
#include <QVBoxLayout>
#include <QTextEdit>
#include <QScrollArea>
#include <QDir>

#include "util.h"

class Console : public QTextEdit
{
    Q_OBJECT
public:
    explicit Console(QWidget *parent = 0);

signals:

public slots:
    void receivedMsg(QString msg);
    void receivedError(QString msg);

private:
};

#endif // CONSOLE_H
