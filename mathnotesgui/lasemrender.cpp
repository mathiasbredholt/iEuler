#include "lasemrender.h"

LASEMRender::LASEMRender(QObject *parent) : QObject(parent)
{
    proc = new QProcess(this);
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
    connect(proc, SIGNAL(finished(int)), this, SLOT(processFinished(int)));
}

void LASEMRender::render(Paragraph *paragraph)
{
    renderQueue.enqueue(paragraph);
    if (renderQueue.size() == 1) {
        proc->start("modules/mathematical/render.rb", QStringList() << renderQueue.head()->latexString);
    }
}

void LASEMRender::readStandardOutput()
{
    qDebug() << proc->readAllStandardOutput();
//    QString output = proc->readAllStandardOutput();
//    output = output.remove("\n");
//    QByteArray by = QByteArray::fromBase64(output.toLatin1());
//    QImage image = QImage::fromData(by, "PNG");
//    currentlyRendering->mathWidget->setPixmap(QPixmap::fromImage(image));
//    if (!renderQueue.isEmpty()) {
//        currentlyRendering = renderQueue.dequeue();
//        proc->write((currentlyRendering->latexString + "\n").toLatin1());
//    }
}

void LASEMRender::readStandardError()
{
    qDebug() << proc->readAllStandardError();
}

void LASEMRender::processFinished(int exitCode)
{
//    QByteArray by = QByteArray::fromBase64(output.toLatin1());
//    QImage image = QImage::fromData(by, "PNG");
//    currentlyRendering->mathWidget->setPixmap(QPixmap::fromImage(image));
    QPixmap image("out.png");
    renderQueue.head()->mathWidget->setPixmap(image);
    renderQueue.dequeue();
    if (!renderQueue.isEmpty()) {
        proc->start("modules/mathematical/render.rb", QStringList() << renderQueue.head()->latexString);
    }
}
