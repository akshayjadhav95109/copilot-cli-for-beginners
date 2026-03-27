using BookApp.Services;

namespace BookApp.Tests;

public class YearValidationTests
{
    [Theory]
    [InlineData(999)]     // Just below minimum
    [InlineData(-1)]      // Negative
    [InlineData(0)]       // Zero
    [InlineData(2101)]    // Just above maximum
    [InlineData(9999)]    // Far in the future
    public void IsValidYear_WithInvalidYears_ShouldReturnFalse(int year)
    {
        Assert.False(YearValidator.IsValidYear(year));
    }

    [Theory]
    [InlineData(1000)]    // Minimum boundary
    [InlineData(1001)]    // Just above minimum
    [InlineData(1949)]    // Classic book year
    [InlineData(2024)]    // Recent year
    [InlineData(2100)]    // Maximum boundary
    public void IsValidYear_WithValidYears_ShouldReturnTrue(int year)
    {
        Assert.True(YearValidator.IsValidYear(year));
    }

    [Theory]
    [InlineData(999, "too early")]
    [InlineData(-1, "too early")]
    [InlineData(0, "too early")]
    [InlineData(2101, "too late")]
    public void GetErrorMessage_ShouldProvideDescriptiveMessage(int year, string expectedPhrase)
    {
        var message = YearValidator.GetErrorMessage(year);
        Assert.Contains(expectedPhrase, message);
        Assert.Contains(year.ToString(), message);
    }

    [Fact]
    public void GetErrorMessage_WithMinBoundary_ShouldMention1000()
    {
        var message = YearValidator.GetErrorMessage(999);
        Assert.Contains("1000", message);
    }

    [Fact]
    public void GetErrorMessage_WithMaxBoundary_ShouldMention2100()
    {
        var message = YearValidator.GetErrorMessage(2101);
        Assert.Contains("2100", message);
    }
}
