import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

// Custom pagination component that displays 3 page number at a time
export function CustomPagination({ currentPage, totalPages, onPageChange }) {
  const renderPageNumbers = () => {
    const pageNumbers = [];
    // Calculate starting page (current page - 1, but not less than 1)
    let startPage = Math.max(1, currentPage - 1);
    // Calculate ending page (start + 2, but not more than total)
    let endPage = Math.min(startPage + 2, totalPages);

    // Adjust start page if we have less than 3 pages to show
    if (endPage - startPage < 2) {
      startPage = Math.max(1, endPage - 2);
    }

    // Generate page numbers for display
    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(
        <PaginationItem key={i}>
          <PaginationLink
            onClick={() => onPageChange(i)}
            isActive={currentPage === i}
            className="cursor-pointer"
          >
            {i}
          </PaginationLink>
        </PaginationItem>
      );
    }
    return pageNumbers;
  };

  // Only show pagination if we have more than 1 page
  return totalPages > 1 ? (
    <Pagination className="mt-4">
      <PaginationContent>
        {/* Previous button - disabled on first page */}
        <PaginationItem>
          <PaginationPrevious
            onClick={() => onPageChange(currentPage - 1)}
            className={
              currentPage === 1
                ? "pointer-events-none opacity-50"
                : "cursor-pointer"
            }
          />
        </PaginationItem>

        {renderPageNumbers()}

        {/* Next button - disabled on last page */}
        <PaginationItem>
          <PaginationNext
            onClick={() => onPageChange(currentPage + 1)}
            className={
              currentPage === totalPages
                ? "pointer-events-none opacity-50"
                : "cursor-pointer"
            }
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  ) : null;
}
