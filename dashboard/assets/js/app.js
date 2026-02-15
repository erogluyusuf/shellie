document.addEventListener('DOMContentLoaded', () => {
    
    // ===============================================
    // BÖLÜM 1: UI VE ETKİLEŞİMLER (Scroll, Tooltip)
    // ===============================================

    // 1. Bootstrap Tooltipleri Başlat
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 2. Smooth Scroll (Sol menüye tıklayınca)
    const navLinks = document.querySelectorAll('#sidebar-nav .nav-link');
    const scrollContainer = document.getElementById('main-scroll');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1); // #sec-cpu -> sec-cpu
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                // Header yüksekliğini (100px) hesaba katarak kaydır
                scrollContainer.scrollTo({
                    top: targetSection.offsetTop - 100, 
                    behavior: 'smooth'
                });
            }
        });
    });

    // 3. ScrollSpy (Elle kaydırınca sol menüyü güncelle)
    scrollContainer.addEventListener('scroll', () => {
        let currentSectionId = "";
        
        // Tüm sectionları gez
        document.querySelectorAll('.section-block').forEach(section => {
            const sectionTop = section.offsetTop - 150; // Tolerans payı
            const sectionHeight = section.clientHeight;
            
            // Eğer scroll pozisyonu bu section aralığındaysa
            if (scrollContainer.scrollTop >= sectionTop && scrollContainer.scrollTop < sectionTop + sectionHeight) {
                currentSectionId = section.getAttribute('id');
            }
        });

        // Linkleri güncelle
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + currentSectionId) {
                link.classList.add('active');
            }
        });
    });

    // ===============================================
    // BÖLÜM 2: API VERİ ÇEKME İŞLEMLERİ (Backend)
    // ===============================================

    // A. SİSTEM İSTATİSTİKLERİNİ GETİR (System.py)
    function fetchSystemStats() {
        fetch('api/system.php')
            .then(response => response.json())
            .then(data => {
                // 1. Genel Bilgiler
                safeUpdate('sys-uptime', data.uptime);
                safeUpdate('sys-hostname', data.hostname);
                safeUpdate('sys-ip', data.ip);
                // Kernel/Platform bilgisini badge içine yazıyoruz
                safeUpdate('sys-platform', data.platform);

                // 2. CPU
                safeUpdate('cpu-percent', data.cpu_percent + "%");
                // Eğer HTML'de cpu-freq adında bir ID varsa güncelle
                if(data.cpu_freq) safeUpdate('cpu-freq', parseInt(data.cpu_freq) + " MHz");
                
                // 3. RAM
                safeUpdate('ram-used', data.ram_used);
                safeUpdate('ram-total', "/ " + data.ram_total);

                // 4. DİSKLER (Dinamik Oluşturma)
                // HTML'de Disk bölümündeki .glass-card içine id="disk-list" eklemeni öneririm.
                // Eğer yoksa, manuel olarak .glass-card içini temizleyip yazarız.
                const diskSection = document.getElementById('sec-disk');
                if (diskSection) {
                    const cardBody = diskSection.querySelector('.glass-card');
                    if (cardBody) {
                        let diskHTML = '';
                        data.disks.forEach(disk => {
                            // Doluluk oranına göre renk değiştir
                            let colorClass = disk.percent > 85 ? 'bg-danger' : (disk.percent > 50 ? 'bg-warning' : 'bg-gradient-primary');
                            
                            diskHTML += `
                                <div class="mb-3">
                                    <div class="d-flex justify-content-between mb-1">
                                        <span>${disk.device}</span>
                                        <span>${disk.used} / ${disk.total}</span>
                                    </div>
                                    <div class="progress bg-secondary bg-opacity-25" style="height: 8px;">
                                        <div class="progress-bar ${colorClass}" style="width: ${disk.percent}%"></div>
                                    </div>
                                </div>
                            `;
                        });
                        // İçeriği güncelle
                        cardBody.innerHTML = diskHTML + `
                             <div class="mt-3 text-end">
                                <button class="btn btn-sm btn-dark border border-secondary text-white-50">Temizle</button>
                            </div>
                        `;
                    }
                }
            })
            .catch(err => console.error("Sistem verisi hatası:", err));
    }

    // B. UYGULAMALARI GETİR (Processes.py)
    function fetchProcesses() {
        fetch('api/processes.php')
            .then(response => response.json())
            .then(data => {
                let html = '';
                // Tablo başlıkları
                html += `
                <table class="table table-dark table-hover mb-0 bg-transparent">
                    <thead><tr><th class="ps-4">App</th><th>CPU</th><th>RAM</th><th class="text-end pe-4">Action</th></tr></thead>
                    <tbody>`;
                
                // Verileri döngüye sok
                data.forEach(proc => {
                    html += `
                        <tr>
                            <td class="ps-4">${proc.name}</td>
                            <td>${proc.cpu.toFixed(1)}%</td>
                            <td>${proc.memory}</td>
                            <td class="text-end pe-4">
                                <button class="btn btn-xs btn-outline-danger border-0"><i class="ph-bold ph-x"></i></button>
                            </td>
                        </tr>
                    `;
                });

                html += `</tbody></table>`;

                // HTML'de #sec-apps içindeki .glass-card'ı bulup bas
                const appSection = document.getElementById('sec-apps');
                if(appSection) {
                    const card = appSection.querySelector('.glass-card');
                    if(card) card.innerHTML = html;
                }
            })
            .catch(err => console.error("Process hatası:", err));
    }

    // C. AĞ DURUMUNU GETİR (Network.py)
    function fetchNetwork() {
        fetch('api/network.php')
            .then(response => response.json())
            .then(data => {
                // HTML'deki ilgili alanları bulmamız lazım.
                // index.php'de bu alanlara id vermemiştik, dinamik bulalım:
                const netSection = document.getElementById('sec-network');
                if (netSection) {
                    const downVal = netSection.querySelector('.border-success .fw-bold');
                    const upVal = netSection.querySelector('.border-primary .fw-bold');
                    
                    if(downVal) downVal.innerHTML = data.download + " <span class='fs-6 fw-normal'>Mbps</span>";
                    if(upVal) upVal.innerHTML = data.upload + " <span class='fs-6 fw-normal'>Mbps</span>";
                }
            })
            .catch(err => console.error("Network hatası:", err));
    }

    // YARDIMCI: ID varsa güncelle, yoksa hata verme
    function safeUpdate(id, value) {
        const el = document.getElementById(id);
        if (el) el.innerText = value;
    }

    // ===============================================
    // BAŞLATMA VE ZAMANLAYICILAR
    // ===============================================

    // İlk yüklemede çalıştır
    fetchSystemStats();
    fetchProcesses();
    fetchNetwork();

    // Periyodik Güncelleme (Zamanlayıcılar)
    setInterval(fetchSystemStats, 2000); // 2 saniyede bir Sistem
    setInterval(fetchNetwork, 3000);     // 3 saniyede bir Ağ
    setInterval(fetchProcesses, 5000);   // 5 saniyede bir Uygulamalar

    console.log("System Dashboard Active & Monitoring...");
});