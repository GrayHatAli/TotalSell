using FluentValidation;
using TotalSell.Application.Commands;

namespace TotalSell.Application.Validators;

public class CreateReportCategoryCommandValidator : AbstractValidator<CreateReportCategoryCommand>
{
    public CreateReportCategoryCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("نام دسته‌بندی الزامی است")
            .MaximumLength(100).WithMessage("نام دسته‌بندی نمی‌تواند بیشتر از 100 کاراکتر باشد");

        RuleFor(x => x.Code)
            .NotEmpty().WithMessage("کد دسته‌بندی الزامی است")
            .MaximumLength(20).WithMessage("کد دسته‌بندی نمی‌تواند بیشتر از 20 کاراکتر باشد")
            .Matches("^[a-zA-Z0-9_-]+$").WithMessage("کد دسته‌بندی باید شامل حروف انگلیسی، اعداد، خط تیره و زیرخط باشد");

        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("توضیحات نمی‌تواند بیشتر از 500 کاراکتر باشد")
            .When(x => x.Description != null);
    }
} 