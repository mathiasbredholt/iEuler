#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{    
    ui->setupUi(this);
    installEventFilter(this);

    numberOfLines = 0;


    // Create tabs
    tabs = new QTabWidget(this);
    tabs->setDocumentMode(true);
    tabs->setTabsClosable(true);
    tabs->setMovable(true);
    ui->container->layout()->addWidget(tabs);
    createNewTab();

    // Create Command panel
    cmdpanel = new CmdPanel(this);
    ui->container->layout()->addWidget(cmdpanel);

    initSubprocess();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::closeEvent(QCloseEvent *e) {
    if (isWindowModified()) {
        QMessageBox msgBox;
        msgBox.setText("The document has been modified.");
        msgBox.setInformativeText("Do you want to save your changes?");
        msgBox.setStandardButtons(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
        msgBox.setDefaultButton(QMessageBox::Save);
        int ret = msgBox.exec();
        if (ret == QMessageBox::Save) saveFile();
        else if (ret == QMessageBox::Cancel) e->ignore();
        else if (ret == QMessageBox::Discard) {
            setWindowModified(false);
        }
    }
}

// Tabs

void MainWindow::createNewTab()
{
    QFrame *contents = new QFrame();
    contents->setLayout(new QVBoxLayout());
    contents->layout()->setAlignment(Qt::AlignTop);
    contents->setBackgroundRole(QPalette::Light);
    contents->setFocusPolicy(Qt::NoFocus);

    QScrollArea *scrollArea = new QScrollArea();
    scrollArea->setWidget(contents);
    scrollArea->setWidgetResizable(true);
    scrollArea->setFocusPolicy(Qt::NoFocus);

    tabs->addTab(scrollArea, "Untitled");
    tabs->setCurrentWidget(scrollArea);
    createGroup();
}


// Groups

void MainWindow::createGroup()
{
    Group* gp = new Group(this, numberOfLines);
    getTabContents()->layout()->addWidget(gp);
    gp->input->setFocus();
    connect(gp->input, SIGNAL(previewCode(CodeInput*, QString)), this, SLOT(previewCode(CodeInput*, QString)));
    connect(gp->input, SIGNAL(evaluateCode(CodeInput*, QString)), this, SLOT(evaluateCode(CodeInput*, QString)));
    connect(gp->input, SIGNAL(deleteGroup(QWidget*)), this, SLOT(deleteGroup(QWidget*)));
    connect(gp->input, SIGNAL(arrowsPressed(bool)), this, SLOT(arrowsPressed(bool)));
    connect(this, SIGNAL(outputReady(int, QString)), gp, SLOT(outputReady(int, QString)));
    numberOfLines++;
}

void MainWindow::deleteGroup(QWidget *target)
{
    if (numberOfLines > 1) {
        focusPreviousChild();
         getTabContents()->layout()->removeWidget(target);
        delete target;
        numberOfLines--;
    }
}

// IO

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
    QString std_out = proc->readAllStandardOutput().simplified();
    int split = std_out.indexOf(' ');
    int line = std_out.left(split).toInt();
    QString latexString = std_out.mid(split);
    latexString = latexString.replace('\n', ' ');
    // send signal to render math
    emit outputReady(line, latexString);
}

void MainWindow::readStandardError()
{
    qDebug() << "python error: \n" << proc->readAllStandardError();
}

void MainWindow::previewCode(CodeInput* target, QString inputString)
{
    QString index = QString::number(((Group*) target->parent())->index);
    inputString = inputString.replace('\n',' ');

    proc->write(index.toLatin1()+"\n");
    proc->write("preview\n");
    proc->write(inputString.toLatin1()+"\n");
//    setWindowModified(true);
}

void MainWindow::evaluateCode(CodeInput* target, QString inputString)
{
    QString index = QString::number(((Group*) target->parent())->index);
    inputString = inputString.replace('\n',' ');

    proc->write(index.toLatin1()+"\n");
    proc->write("evaluate\n");
    proc->write(inputString.toLatin1()+"\n");
    if (((Group*) target->parent())->index == numberOfLines-1) {
        createGroup();
    }
}

// File I/O

void MainWindow::openFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getOpenFileName(this,
        tr("Open iEuler file"), dir, tr("Text Files (*.txt)"));
    if (path != "") {
        qDebug() << path;
    //    proc->write("open\n");
    //    proc->write(path+"\n");
    }
}

void MainWindow::saveFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
        tr("Save iEuler file"), dir, tr("Text Files (*.txt)"));
    qDebug() << path;
//    proc->write("save\n");
//    proc->write(path+"\n");
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

void MainWindow::on_action100_triggered()
{
    MathRenderer::ZOOM_FACTOR = 1;
}

void MainWindow::on_action150_triggered()
{
    MathRenderer::ZOOM_FACTOR = 1.5;
}

void MainWindow::on_action200_triggered()
{
    MathRenderer::ZOOM_FACTOR = 2;
}

void MainWindow::on_actionNew_triggered()
{
    createNewTab();
}

void MainWindow::on_actionClose_triggered()
{
    if (tabs->count() > 1) {
        tabs->setCurrentIndex(tabs->currentIndex() - 1);
        tabs->removeTab(tabs->currentIndex() + 1);
    }
}

QWidget* MainWindow::getTabContents() {
    return ((QScrollArea*) tabs->currentWidget())->widget();
}

void MainWindow::on_actionOpen_triggered()
{
    openFile();
}

void MainWindow::on_actionSave_triggered()
{
    saveFile();
}
