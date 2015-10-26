#ifndef CUSTOMFRAME_H
#define CUSTOMFRAME_H

#include <QObject>
#include <QWidget>
#include <QFrame>
#include <QWheelEvent>
#include <QDebug>

class CustomFrame : public QFrame
{
    Q_OBJECT
public:
    CustomFrame();

private:
    bool eventFilter(QObject *object, QEvent *e);

};

#endif // CUSTOMFRAME_H
