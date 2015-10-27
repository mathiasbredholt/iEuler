#ifndef MATHRENDERER_H
#define MATHRENDERER_H

#include <QObject>
#include <QWebView>

class MathRenderer : public QObject
{
    Q_OBJECT
public:
    static qreal ZOOM_FACTOR;

    explicit MathRenderer(QObject *parent = 0);
    QWebView *view;
    void render(QString latexString);

signals:

public slots:
    void hasLoaded();


private:
    bool isReady;
    bool eventFilter(QObject *object, QEvent *event);

private slots:
};

#endif // MATHRENDERER_H
