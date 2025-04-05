using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class DeleteReportCategoryCommandValidator : AbstractValidator<DeleteReportCategoryCommand>
{
    public DeleteReportCategoryCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("شناسه دسته‌بندی الزامی است");
    }
} 