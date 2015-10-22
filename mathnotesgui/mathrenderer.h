#ifndef MATHRENDERER_H
#define MATHRENDERER_H

#include <QObject>
#include <QWebView>

class MathRenderer : public QObject
{
    Q_OBJECT
public:
    explicit MathRenderer(QObject *parent = 0);
    QWebView *view;
    void render(QString *latexString);

signals:

public slots:
};

#endif // MATHRENDERER_H
