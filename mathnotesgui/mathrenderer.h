#ifndef MATHRENDERER_H
#define MATHRENDERER_H

#include <QObject>

class MathRenderer : public QObject
{
    Q_OBJECT
public:
    explicit MathRenderer(QObject *parent = 0);

signals:

public slots:
};

#endif // MATHRENDERER_H
