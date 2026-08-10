/** @odoo-module **/

import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import { uiService } from "@web/core/ui/ui_service";

/**
 * XLSX Handler
 * Mengunduh laporan berformat XLSX via controller '/xlsx_reports'
 */
registry.category("ir.actions.report handlers").add(
    "hotel_xlsx", // ✅ Solusi Utama: Gunakan nama unik agar tidak terjadi bentrok key "xlsx"
    async function (action, options, env) {
        if (action.report_type === "xlsx") {
            // Blokir UI selama pengunduhan berjalan
            env.services.ui.block();

            try {
                await download({
                    url: "/xlsx_reports",
                    data: action.data,
                });
            } catch (error) {
                // Tampilkan error bawaan Odoo jika terjadi kesalahan
                if (env.services.notification) {
                    env.services.notification.add(
                        error.message || "Gagal mengunduh laporan XLSX",
                        { type: "danger" }
                    );
                }
            } finally {
                // Buka kembali UI setelah pengunduhan selesai/gagal
                env.services.ui.unblock();
            }

            // Kembalikan true untuk menandai bahwa action ini sudah ditangani
            return true;
        }

        // Kembalikan false agar handler lain bisa mengecek jika tipe laporan bukan 'xlsx'
        return false;
    }
);