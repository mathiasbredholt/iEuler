#ifndef LASEMRENDER_H
#define LASEMRENDER_H

#include <QObject>
#include <QProcess>
#include <QDebug>
#include <QQueue>

#include "paragraph.h"

class LASEMRender : public QObject
{
    Q_OBJECT
public:
    explicit LASEMRender(QObject *parent = 0);

private:
    QQueue<Paragraph*> renderQueue;
    QProcess *proc;

signals:

public slots:
    void render(Paragraph *paragraph);

private slots:
    void readStandardOutput();
    void readStandardError();
    void processFinished(int);
};

#endif // LASEMRENDER_H
