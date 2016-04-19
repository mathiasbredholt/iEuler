#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
    installEventFilter(this);

    setupUIParameters();
    createFileMenu();
    createToolsMenu();
    createContainer();

    euler = new Euler();
    connect(euler, SIGNAL(receivedMathString(int, int, QString)), this, SLOT(receivedMathString(int, int, QString)));

    renderer = new Renderer(minimumWidth(),minimumHeight());
    renderer->windowWidth = minimumWidth();

//     Create/ tabs
    tabs = new QTabWidget(this);
    tabs->setDocumentMode(true);
    tabs->setTabsClosable(true);
    tabs->setStyleSheet("QTabWidget { left: 5px; border: none; background: #FFF; /* move to the right by 5px */ } QTabBar::tab { font: Monaco; color: white; background: #666; } QTabBar::tab:selected { background: #444 }");
    tabs->setMovable(true);
    container->layout()->addWidget(tabs);

    createNewTab();

    // Create workspace
    workspace = new Workspace(this);
    container->layout()->addWidget(workspace);
    connect(euler, SIGNAL(receivedWorkspace(int,int,QVariantMap)), workspace, SLOT(receivedWorkspace(int,int,QVariantMap)));

//     Create Command panel
    cmdpanel = new CmdPanel(this);
    container->layout()->addWidget(cmdpanel);

    // Create console
    console = new Console(this);
    container->layout()->addWidget(console);
    connect(euler, SIGNAL(receivedMsg(QString)), console, SLOT(receivedMsg(QString)));
    connect(euler, SIGNAL(receivedError(QString)), console, SLOT(receivedError(QString)));

}

MainWindow::~MainWindow()
{
//    delete ui;
}

void MainWindow::createToolsMenu()
{
    QMenu *toolsMenu = menuBar()->addMenu(tr("&Tools"));

    // Zoom
    QAction *zoom100 = new QAction(tr("&Zoom 100%"), this);
    zoom100->setShortcut(QKeySequence(tr("Ctrl+1")));
    connect(zoom100, SIGNAL(triggered(bool)), this, SLOT(on_action100_triggered()));
    toolsMenu->addAction(zoom100);

    QAction *zoom150 = new QAction(tr("&Zoom 150%"), this);
    zoom150->setShortcut(QKeySequence(tr("Ctrl+2")));
    connect(zoom150, SIGNAL(triggered(bool)), this, SLOT(on_action150_triggered()));
    toolsMenu->addAction(zoom150);

    QAction *zoom200 = new QAction(tr("&Zoom 200%"), this);
    zoom200->setShortcut(QKeySequence(tr("Ctrl+3")));
    connect(zoom200, SIGNAL(triggered(bool)), this, SLOT(on_action200_triggered()));
    toolsMenu->addAction(zoom200);
}

void MainWindow::setupUIParameters()
{
    QGuiApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    setMinimumSize(ptX(600), ptY(600));

    pal = palette();

//    Dark theme
//    pal.setColor(QPalette::Base, QColor("#333"));
//    pal.setColor(QPalette::Background, QColor("#333"));
//    pal.setColor(QPalette::Text, QColor("#FFF"));

    pal.setColor(QPalette::Base, QColor("#FFF"));
    pal.setColor(QPalette::Background, QColor("#FFF"));
    pal.setColor(QPalette::Text, QColor("#000"));

    setPalette(pal);

    setFont(QFont("Monaco", 12));
}

void MainWindow::createContainer()
{
    container = new QWidget(this);
    container->setLayout(new QVBoxLayout());
    container->layout()->setMargin(0);
    setCentralWidget(container);
}

void MainWindow::createFileMenu()
{
    QMenu *fileMenu = menuBar()->addMenu(tr("&File"));

    // Open menu
    QAction *newAct = new QAction(tr("&New"), this);
    newAct->setShortcut(QKeySequence(tr("Ctrl+N")));
    connect(newAct, SIGNAL(triggered(bool)), this, SLOT(on_actionNew_triggered()));
    fileMenu->addAction(newAct);


    // Open menu
    QAction *openAct = new QAction(tr("&Open"), this);
    openAct->setShortcut(QKeySequence(tr("Ctrl+O")));
    connect(openAct, SIGNAL(triggered(bool)), this, SLOT(on_actionOpen_triggered()));
    fileMenu->addAction(openAct);

    // Save menu
    QAction *saveAct = new QAction(tr("&Save"), this);
    saveAct->setShortcut(QKeySequence(tr("Ctrl+S")));
    connect(saveAct, SIGNAL(triggered(bool)), this, SLOT(on_actionSave_triggered()));
    fileMenu->addAction(saveAct);

    // Close menu
    QAction *closeAct = new QAction(tr("&Close"), this);
    closeAct->setShortcut(QKeySequence(tr("Ctrl+W")));
    connect(closeAct, SIGNAL(triggered(bool)), this, SLOT(on_actionClose_triggered()));
    fileMenu->addAction(closeAct);

    // Restart core
    QAction *coreAct = new QAction(tr("&Restart core"), this);
    coreAct->setShortcut(QKeySequence(tr("Ctrl+R")));
    connect(coreAct, SIGNAL(triggered(bool)), this, SLOT(on_actionRestart_core_triggered()));
    fileMenu->addAction(coreAct);
}

void MainWindow::initRenderer() {
    renderer->move(this->pos());
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
    } else {
        euler->terminate();
        renderer->close();
        qDebug() << "Terminate python.";
    }
}

void MainWindow::moveEvent(QMoveEvent *event)
{
    renderer->move(pos());
}

void MainWindow::scrollTo(Paragraph *paragraph)
{
    ((QScrollArea*) tabs->currentWidget())->ensureWidgetVisible(paragraph, 0, 400);
}

// Tabs

void MainWindow::createNewTab(bool empty, QString fileName)
{
    QFrame *contents = new QFrame(this);
    QVBoxLayout *layout = new QVBoxLayout;
    layout->setContentsMargins(ptY(10), ptY(10), ptY(10), ptY(256));
    layout->setAlignment(Qt::AlignTop);
    contents->setLayout(layout);
    contents->setPalette(pal);
    contents->setFocusPolicy(Qt::NoFocus);

    QScrollArea *scrollArea = new QScrollArea(this);
    scrollArea->setWidget(contents);
    scrollArea->setWidgetResizable(true);
    scrollArea->setFocusPolicy(Qt::NoFocus);
//    scrollArea->setSizeAdjustPolicy(QAbstractScrollArea::AdjustToContents);
    scrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    contents->show();

    tabs->addTab(scrollArea, fileName);
    tabs->setCurrentWidget(scrollArea);
    connect(tabs, SIGNAL(tabBarClicked(int)), this, SLOT(onTabChange(int)));
    setWindowTitle("iEuler - "+fileName);

    numberOfLines = 0;
    if (!empty) addNewParagraph();
}


void MainWindow::addNewParagraph(QString mathString)
{
    int tabIndex = tabs->currentIndex();
    int index = numberOfLines;
    Paragraph *paragraph = new Paragraph(this,
                                         euler,
                                         renderer,
                                         tabIndex,
                                         index,
                                         mathString);

    getTabContents()->layout()->addWidget(paragraph);
    connect(paragraph, SIGNAL(changeFocus_triggered(Paragraph*,bool)), this, SLOT(changeFocus_triggered(Paragraph*,bool)));
    connect(paragraph, SIGNAL(newLine_triggered(int)), this, SLOT(newLine_triggered(int)));
    connect(paragraph, SIGNAL(deleteLine_triggered(Paragraph*)), this, SLOT(deleteLine_triggered(Paragraph*)));

    numberOfLines++;
    paragraph->focus();

    qApp->processEvents();
    scrollTo(paragraph);
}

void MainWindow::newLine_triggered(int index)
{
    if (index == numberOfLines - 1) {
        addNewParagraph();
    }
}

void MainWindow::deleteLine_triggered(Paragraph *target)
{
    if (numberOfLines > 1) {
        focusPreviousChild();
        getTabContents()->layout()->removeWidget(target);
        delete target;
        numberOfLines--;
    }
}


// File I/O

void MainWindow::openFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getOpenFileName(this,
        tr("Open iEuler file"), dir, tr("iEuler files (*.eulerc)"));
    if (path != "") {
        QFileInfo fi(path);
        createNewTab(true, fi.baseName());

        euler->sendOpenFileRequest(path);
    }

}

void MainWindow::saveFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
        tr("Save iEuler file"), dir, tr("Text Files (*.euler)"));

    if (path != "") {
        QFileInfo fi(path);
        euler->sendSaveFileRequest(path);
        tabs->setTabText(tabs->currentIndex(), fi.baseName());
        setWindowTitle("iEuler - "+fi.baseName());
    }
}

void MainWindow::exportFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
        tr("Export PDF file"), dir, tr("PDF Files (*.pdf)"));

    if (path != "") {
        euler->sendExportRequest(path);
    }
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

void MainWindow::changeFocus_triggered(Paragraph *paragraph, bool goUp)
{
    scrollTo(paragraph);
    if (goUp) {
        if (paragraph->index > 0) focusPreviousChild();
    } else {
        if (paragraph->index < numberOfLines-1) focusNextChild();
    }
}

void MainWindow::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_Escape) {
        cmdpanel->hide();
    }
}

void MainWindow::receivedMathString(int tabIndex, int index, QString mathString)
{
    addNewParagraph(mathString);
}

void MainWindow::on_action100_triggered()
{
    renderer->setZoomFactor(100);
}

void MainWindow::on_action150_triggered()
{
    renderer->setZoomFactor(150);
}

void MainWindow::on_action200_triggered()
{
    renderer->setZoomFactor(200);
}

void MainWindow::on_actionNew_triggered()
{
    createNewTab();
}

void MainWindow::on_actionClose_triggered()
{
    if (tabs->currentIndex() > 0) {
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

void MainWindow::on_actionExport_triggered()
{
    exportFile();
}

void MainWindow::onTabChange(int index)
{
    setWindowTitle("iEuler - "+tabs->tabText(index));
}

void MainWindow::on_actionRestart_core_triggered()
{
    euler->restartCore();
}
