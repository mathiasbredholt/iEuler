#include "mainwindow.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{    
    ui->setupUi(this);
    installEventFilter(this);

    numberOfLines = 0;
    cmdpanel = new CmdPanel(this);

    ui->container->layout()->addWidget(cmdpanel);
    ui->content->layout()->setAlignment(Qt::AlignTop);

    createNewCodeLine();

    initSubprocess();
}

void MainWindow::initSubprocess()
{
    proc = new QProcess(this);
    proc->start("python3 start.py -gui");
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
}

void MainWindow::readStandardOutput()
{
    // get line number and latex string from ieuler
    QString stdout = proc->readAllStandardOutput();
    int split = stdout.indexOf(' ');
    int line = stdout.left(split).toInt();
    QString latexString = stdout.mid(split);
    // send signal to render math
    emit outputReady(line, latexString);
}

void MainWindow::readStandardError()
{
    qDebug() << "python error: \n" << proc->readAllStandardError();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::evaluateCode(CodeInput* target, QString inputString)
{
    inputString = inputString.replace('\n',' ');
    proc->write(QString::number(((Group*) target->parent())->index).toLatin1()+"\n"+inputString.toLatin1()+"\n");
    if (((Group*) target->parent())->index == numberOfLines-1) {
//        createNewCodeLine();
    }
}

void MainWindow::deleteGroup(QWidget *target)
{
    if (numberOfLines > 1) {
        focusPreviousChild();
        ui->content->layout()->removeWidget(target);
        delete target;
        numberOfLines--;
    }
}


void MainWindow::createNewCodeLine()
{
    Group* gp = new Group(this, numberOfLines);
    ui->content->layout()->addWidget(gp);
    gp->input->setFocus();
    connect(gp->input, SIGNAL(evaluateCode(CodeInput*, QString)), this, SLOT(evaluateCode(CodeInput*, QString)));
    connect(gp->input, SIGNAL(deleteGroup(QWidget*)), this, SLOT(deleteGroup(QWidget*)));
    connect(gp->input, SIGNAL(arrowsPressed(bool)), this, SLOT(arrowsPressed(bool)));
    connect(this, SIGNAL(outputReady(int, QString)), gp, SLOT(outputReady(int, QString)));
    numberOfLines++;
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

void MainWindow::arrowsPressed(bool upArrowPressed)
{
    int index = ((Group*) focusWidget()->parent())->index;
    if (upArrowPressed) {
        if (index > 0) focusPreviousChild();
    } else {
        if (index < numberOfLines-1) focusNextChild();
    }
}

void MainWindow::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_Escape) {
        cmdpanel->hide();
    }
}
