#ifndef EDITOR_H
#define EDITOR_H

#include <QLineEdit>
#include <QKeyEvent>
#include <QEvent>
#include <QTextBlock>

class Editor : public QLineEdit
{
    Q_OBJECT
public:
    explicit Editor(QWidget *parent = 0);

signals:

public slots:

private slots:
    bool eventFilter(QObject *object, QEvent *event);
};

#endif // EDITOR_H

