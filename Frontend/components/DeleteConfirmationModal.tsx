import React from 'react';
import { X, AlertTriangle } from 'lucide-react';

interface DeleteConfirmationModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void;
    chatTitle: string;
    isDeleting: boolean;
}

export const DeleteConfirmationModal: React.FC<DeleteConfirmationModalProps> = ({
    isOpen,
    onClose,
    onConfirm,
    chatTitle,
    isDeleting
}) => {
    if (!isOpen) return null;

    const handleBackdropClick = (e: React.MouseEvent) => {
        if (e.target === e.currentTarget && !isDeleting) {
            onClose();
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Escape' && !isDeleting) {
            onClose();
        }
    };

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200"
            onClick={handleBackdropClick}
            onKeyDown={handleKeyDown}
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-modal-title"
        >
            <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8 animate-in slide-in-from-bottom-4 duration-300">
                {/* Header */}
                <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-red-600" />
                        </div>
                        <h2 id="delete-modal-title" className="text-2xl font-bold text-[#1E1E1E]">
                            Delete Chat
                        </h2>
                    </div>
                    {!isDeleting && (
                        <button
                            onClick={onClose}
                            className="p-2 text-[#555555] hover:text-[#1E1E1E] transition-colors rounded-lg hover:bg-[#FAFAF7]"
                            aria-label="Close modal"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    )}
                </div>

                {/* Content */}
                <div className="mb-8">
                    <p className="text-[#555555] text-base leading-relaxed mb-4">
                        Are you sure you want to permanently delete this chat?
                    </p>
                    <div className="bg-[#FAFAF7] border border-[#E6E6E6] rounded-xl p-4">
                        <p className="text-sm font-semibold text-[#1E1E1E] mb-1">
                            Chat Title:
                        </p>
                        <p className="text-sm text-[#555555] truncate">
                            {chatTitle}
                        </p>
                    </div>
                    <p className="text-sm text-red-600 font-medium mt-4 flex items-center gap-2">
                        <AlertTriangle className="w-4 h-4" />
                        This action cannot be undone. All messages will be permanently deleted.
                    </p>
                </div>

                {/* Actions */}
                <div className="flex gap-3">
                    <button
                        onClick={onClose}
                        disabled={isDeleting}
                        className="flex-1 py-3 px-4 bg-[#FAFAF7] border border-[#E6E6E6] text-[#555555] rounded-xl font-bold hover:bg-[#E6E6E6] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={onConfirm}
                        disabled={isDeleting}
                        className="flex-1 py-3 px-4 bg-red-600 text-white rounded-xl font-bold hover:bg-red-700 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {isDeleting ? (
                            <>
                                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                Deleting...
                            </>
                        ) : (
                            'Delete'
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

