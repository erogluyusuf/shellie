<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor - Dark Aurora</title>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <div class="app-container">
        
        <aside class="sidebar-area">
            <div class="aurora-panel d-flex flex-column align-items-center justify-content-center py-3">
                <nav class="nav flex-column gap-3 w-100 align-items-center" id="sidebar-nav">
                    <a href="#sec-overview" class="nav-link active" data-bs-toggle="tooltip" data-bs-placement="right" title="Genel Bakış"><i class="ph-bold ph-squares-four"></i></a>
                    <a href="#sec-cpu" class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="CPU"><i class="ph-bold ph-cpu"></i></a>
                    <a href="#sec-ram" class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="RAM"><i class="ph-bold ph-memory"></i></a>
                    <a href="#sec-disk" class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Disk"><i class="ph-bold ph-hard-drives"></i></a>
                    <a href="#sec-apps" class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Uygulamalar"><i class="ph-bold ph-stack"></i></a>
                    <a href="#sec-network" class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Ağ"><i class="ph-bold ph-globe-hemisphere-west"></i></a>
                    <a href="#sec-security" class="nav-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Güvenlik"><i class="ph-bold ph-shield-check"></i></a>
                    <div style="height: 10px;"></div>
                    <a href="#sec-utils" class="nav-link text-warning" data-bs-toggle="tooltip" data-bs-placement="right" title="Araçlar"><i class="ph-bold ph-wrench"></i></a>
                </nav>
                <div class="mt-auto mb-2">
                     <a href="#" class="nav-link text-danger" title="Çıkış"><i class="ph-bold ph-power"></i></a>
                </div>
            </div>
        </aside>

        <main class="aurora-panel position-relative overflow-hidden">
            
            <div class="scroll-container p-4" id="main-scroll">
                
                <div class="d-flex justify-content-between align-items-center mb-5 sticky-top p-3 glass-header rounded-4">
                    <h2 class="fw-light m-0 fs-4 text-white">System Monitor</h2>
                    <div id="sys-platform" class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-25 px-3 py-2">
                        <i class="ph-fill ph-circle me-2"></i> Sistem Taranıyor...
                    </div>
                </div>

                <section id="sec-overview" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-squares-four me-2"></i> Genel Sistem</h4>
                    <div class="row g-3">
                        <div class="col-md-3">
                            <div class="glass-card p-3 text-center">
                                <small class="text-white-50">Uptime</small>
                                <h3 id="sys-uptime" class="my-2">--</h3>
                                <span class="badge bg-white bg-opacity-10">Online</span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="glass-card p-3 text-center">
                                <small class="text-white-50">Durum</small>
                                <h3 class="my-2 text-info">Aktif</h3>
                                <div class="progress" style="height: 4px;"><div class="progress-bar bg-info" style="width: 100%"></div></div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="glass-card p-3 d-flex justify-content-between align-items-center">
                                <div class="text-start"><small class="text-white-50 d-block">IP Adresi</small><span id="sys-ip" class="fs-5 font-monospace">...</span></div>
                                <div class="text-end"><small class="text-white-50 d-block">Hostname</small><span id="sys-hostname" class="fs-5">...</span></div>
                            </div>
                        </div>
                    </div>
                </section>

                <section id="sec-cpu" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-cpu me-2"></i> CPU</h4>
                    <div class="glass-card p-4">
                        <div class="d-flex justify-content-between mb-3">
                            <div><h2 id="cpu-percent" class="display-4 fw-bold mb-0">0%</h2><small id="cpu-freq" class="text-white-50">Hesaplanıyor...</small></div>
                            <div class="text-end"><div class="fs-3 text-warning"><i class="ph-fill ph-thermometer"></i> --°C</div></div>
                        </div>
                        <div class="d-flex align-items-end gap-1" style="height: 60px;">
                            <div class="bg-primary w-100 rounded-top opacity-50" style="height: 20%"></div>
                            <div class="bg-primary w-100 rounded-top opacity-75" style="height: 45%"></div>
                            <div class="bg-primary w-100 rounded-top" style="height: 30%"></div>
                            <div class="bg-primary w-100 rounded-top opacity-50" style="height: 60%"></div>
                            <div class="bg-primary w-100 rounded-top opacity-75" style="height: 10%"></div>
                        </div>
                    </div>
                </section>

                <section id="sec-ram" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-memory me-2"></i> RAM</h4>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="glass-card p-4 text-center">
                                <div id="ram-used" class="fs-3 fw-bold text-white mb-2">-- GB</div>
                                <small id="ram-total" class="text-white-50">/ -- GB</small>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="glass-card p-3 d-flex flex-column justify-content-center">
                                <div class="text-center text-white-50">
                                    <i class="ph-duotone ph-chart-bar fs-1 mb-2"></i>
                                    <p>Detaylı analiz için Uygulamalar sekmesine bakınız.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section id="sec-disk" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-hard-drives me-2"></i> Disk</h4>
                    <div class="glass-card p-4">
                        <div class="text-center text-white-50">Yükleniyor...</div>
                    </div>
                </section>

                <section id="sec-apps" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-stack me-2"></i> Uygulamalar</h4>
                    <div class="glass-card p-0 overflow-hidden">
                         <div class="text-center py-4 text-white-50">Veriler alınıyor...</div>
                    </div>
                </section>

                <section id="sec-network" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-globe-hemisphere-west me-2"></i> Ağ</h4>
                    <div class="row g-3">
                        <div class="col-6">
                            <div class="glass-card p-3 border-start border-4 border-success">
                                <span class="text-white-50">Download</span>
                                <div class="fs-4 fw-bold">-- Mbps</div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="glass-card p-3 border-start border-4 border-primary">
                                <span class="text-white-50">Upload</span>
                                <div class="fs-4 fw-bold">-- Mbps</div>
                            </div>
                        </div>
                    </div>
                </section>

                <section id="sec-security" class="mb-5 section-block">
                    <h4 class="section-title"><i class="ph-bold ph-shield-check me-2"></i> Güvenlik</h4>
                    <div class="glass-card p-3 d-flex justify-content-between mb-2">
                        <div><i class="ph-fill ph-fire text-success me-2"></i> Firewall</div>
                        <span class="badge bg-success">Aktif</span>
                    </div>
                    <div class="glass-card p-3 d-flex justify-content-between">
                        <div><i class="ph-fill ph-bug-beetle text-warning me-2"></i> Defender</div>
                        <span class="badge bg-warning text-dark">İzleniyor</span>
                    </div>
                </section>

                <section id="sec-utils" class="mb-5 section-block">
                    <h4 class="section-title text-warning"><i class="ph-bold ph-wrench me-2"></i> Araçlar</h4>
                    <div class="glass-card p-4">
                        <div class="row g-3">
                            <div class="col-4"><button class="btn btn-outline-danger w-100 py-3 app-btn"><i class="ph-bold ph-lightning fs-4 mb-2 d-block"></i>SHOCK</button></div>
                            <div class="col-4"><button class="btn btn-outline-warning w-100 py-3 app-btn"><i class="ph-bold ph-broom fs-4 mb-2 d-block"></i>Clean</button></div>
                            <div class="col-4"><button class="btn btn-outline-info w-100 py-3 app-btn"><i class="ph-bold ph-arrows-clockwise fs-4 mb-2 d-block"></i>Restart</button></div>
                        </div>
                    </div>
                </section>
                
                <div style="height: 50px;"></div>
            </div>
        </main>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="assets/js/app.js"></script>
</body>
</html>