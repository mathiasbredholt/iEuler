#ifndef MATHRENDERER_H
#define MATHRENDERER_H

#include <QObject>
#include <QWebView>
#include <QLabel>
#include <QQueue>

class MathRenderer : public QObject
{
    Q_OBJECT
public:
    static qreal zoomFactor;
    static qreal baseScaling;
    static void initRenderer();
    static QQueue<MathRenderer*> renderQueue;
    static void render();
    static bool isRendering;
    static bool isReady;


    explicit MathRenderer(QObject *parent = 0);
    QLabel *label;
    QString latexString;

signals:

public slots:
    void hasLoaded();
    void hasRendered();
    void toggleRendering(bool disable);

private:
    static QWebView *renderer;

private slots:
};

#endif // MATHRENDERER_H
